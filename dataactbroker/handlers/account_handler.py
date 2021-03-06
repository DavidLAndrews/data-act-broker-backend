import logging
from operator import attrgetter
import requests
import xmltodict

from flask import g

from dataactbroker.handlers.aws.sesEmail import SesEmail
from dataactbroker.handlers.aws.session import LoginSession
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.requestDictionary import RequestDictionary
from dataactcore.utils.responseException import ResponseException
from dataactcore.interfaces.db import GlobalDB
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import func

from dataactcore.models.userModel import User, UserAffiliation
from dataactcore.models.domainModels import CGAC, FREC
from dataactcore.models.jobModels import Submission
from dataactcore.utils.statusCode import StatusCode
from dataactcore.interfaces.function_bag import get_email_template, check_correct_password
from dataactcore.config import CONFIG_BROKER
from dataactcore.models.lookups import PERMISSION_SHORT_DICT, DABS_PERMISSION_ID_LIST, FABS_PERMISSION_ID_LIST


logger = logging.getLogger(__name__)


class AccountHandler:
    """ This class contains the login / logout  functions

        Attributes:
            is_local: A boolean indicating if the application is being run locally or not
            request: A Flask object containing the data from the request
            bcrypt: A Bcrypt object associated with the app

        Constants:
            FRONT_END: A string indicating the URL of the front end of the app
    """
    # Handles login process, compares username and password provided
    FRONT_END = ""
    # Instance fields include request, response, logFlag, and logFile

    def __init__(self, request, bcrypt=None, is_local=False):
        """ Creates the Login Handler

            Args:
                request: Flask request object
                bcrypt: Bcrypt object associated with app
        """
        self.is_local = is_local
        self.request = request
        self.bcrypt = bcrypt

    def login(self, session):
        """ Logs a user in if their password matches using local data

            Args:
                session: the Session object from flask

            Returns:
                A JsonResponse containing the user information or details on which error occurred, such as whether a
                type was wrong, something wasn't implemented, invalid keys were provided, login was denied, or a
                different, unexpected error occurred.
        """
        try:
            sess = GlobalDB.db().session
            safe_dictionary = RequestDictionary(self.request)

            username = safe_dictionary.get_value('username')
            password = safe_dictionary.get_value('password')

            try:
                user = sess.query(User).filter(func.lower(User.email) == func.lower(username)).one()
            except Exception:
                raise ValueError("Invalid username and/or password")

            try:
                if check_correct_password(user, password, self.bcrypt):
                    # We have a valid login
                    return self.create_session_and_response(session, user)
                else:
                    raise ValueError("Invalid username and/or password")
            except ValueError as ve:
                LoginSession.logout(session)
                raise ve
            except Exception as e:
                LoginSession.logout(session)
                raise e

        # Catch any specifically raised errors or any other errors that may have happened and return them cleanly
        except (TypeError, KeyError, NotImplementedError) as e:
            # Return a 400 with appropriate message
            return JsonResponse.error(e, StatusCode.CLIENT_ERROR)
        except ValueError as e:
            # Return a 401 for login denied
            return JsonResponse.error(e, StatusCode.LOGIN_REQUIRED)
        except Exception as e:
            # Return 500
            return JsonResponse.error(e, StatusCode.INTERNAL_ERROR)

    def max_login(self, session):
        """ Logs a user in if their password matches using MAX

            Args:
                session: Session object from flask

            Returns:
                A JsonResponse containing the user information or details on which error occurred, such as whether a
                type was wrong, something wasn't implemented, invalid keys were provided, login was denied, or a
                different, unexpected error occurred.
        """
        try:
            safe_dictionary = RequestDictionary(self.request)

            ticket = safe_dictionary.get_value("ticket")
            service = safe_dictionary.get_value('service')

            # Call MAX's serviceValidate endpoint and retrieve the response
            max_dict = get_max_dict(ticket, service)

            if 'cas:authenticationSuccess' not in max_dict['cas:serviceResponse']:
                raise ValueError("You have failed to login successfully with MAX")
            cas_attrs = max_dict['cas:serviceResponse']['cas:authenticationSuccess']['cas:attributes']

            # Grab MAX ID to see if a service account is being logged in
            max_id_components = cas_attrs['maxAttribute:MAX-ID'].split('_')
            service_account_flag = (len(max_id_components) > 1 and max_id_components[0].lower() == 's')

            # Grab the email and list of groups from MAX's response
            email = cas_attrs['maxAttribute:Email-Address']

            try:
                sess = GlobalDB.db().session
                user = sess.query(User).filter(func.lower(User.email) == func.lower(email)).one_or_none()

                # If the user does not exist, create them since they are allowed to access the site because they got
                # past the above group membership checks
                if user is None:
                    user = User()
                    user.email = email

                set_user_name(user, cas_attrs)

                set_max_perms(user, cas_attrs['maxAttribute:GroupList'], service_account_flag)

                sess.add(user)
                sess.commit()

            except MultipleResultsFound:
                raise ValueError("An error occurred during login.")

            return self.create_session_and_response(session, user)

        # Catch any specifically raised errors or any other errors that may have happened and return them cleanly
        except (TypeError, KeyError, NotImplementedError) as e:
            # Return a 400 with appropriate message
            return JsonResponse.error(e, StatusCode.CLIENT_ERROR)
        except ValueError as e:
            # Return a 401 for login denied
            return JsonResponse.error(e, StatusCode.LOGIN_REQUIRED)
        except Exception as e:
            # Return 500
            return JsonResponse.error(e, StatusCode.INTERNAL_ERROR)

    @staticmethod
    def create_session_and_response(session, user):
        """ Create a session.

            Args:
                session: Session object from flask
                user: Users object

            Returns:
                JsonResponse containing the JSON for the user
        """
        LoginSession.login(session, user.user_id)
        data = json_for_user(user, session['sid'])
        data['message'] = 'Login successful'
        return JsonResponse.create(StatusCode.OK, data)

    def set_skip_guide(self):
        """ Set current user's skip guide parameter

            Returns:
                JsonResponse object containing results of setting the skip guide or details of the error that occurred.
                Possible errors include the request not containing a skip_guide parameter or it not being a boolean
                value
        """
        sess = GlobalDB.db().session
        request_dict = RequestDictionary.derive(self.request)
        try:
            if 'skip_guide' not in request_dict:
                raise ResponseException(
                    "Must include skip_guide parameter",
                    StatusCode.CLIENT_ERROR
                )
            skip_guide = str(request_dict['skip_guide']).lower()
            if skip_guide not in ("true", "false"):
                raise ResponseException(
                    "skip_guide must be true or false",
                    StatusCode.CLIENT_ERROR
                )
            g.user.skip_guide = skip_guide == "true"
        except ResponseException as exc:
            return JsonResponse.error(exc, exc.status)
        sess.commit()
        return JsonResponse.create(StatusCode.OK, {"message": "skip_guide set successfully", "skip_guide": skip_guide})

    def email_users(self, system_email):
        """ Send email notification to list of users

            Args:
                system_email: the address of the system to send the email from

            Returns:
                A JsonReponse containing a message that the email sent successfully or the details of the missing
                parameters
        """
        sess = GlobalDB.db().session
        request_dict = RequestDictionary.derive(self.request)
        required = ('users', 'submission_id', 'email_template')
        try:
            if any(field not in request_dict for field in required):
                raise ResponseException(
                    "Email users route requires users, email_template, and submission_id", StatusCode.CLIENT_ERROR
                )
        except ResponseException as exc:
            return JsonResponse.error(exc, exc.status)

        user_ids = request_dict['users']
        submission_id = request_dict['submission_id']
        # Check if submission id is valid
        _, agency_name = sess.query(Submission.submission_id, CGAC.agency_name).\
            join(CGAC, Submission.cgac_code == CGAC.cgac_code).filter(Submission.submission_id == submission_id).one()
        if not agency_name:
            _, agency_name = sess.query(Submission.submission_id, FREC.agency_name).\
                join(FREC, Submission.frec_code == FREC.frec_code).\
                filter(Submission.submission_id == submission_id).one()

        template_type = request_dict['email_template']
        # Check if email template type is valid
        get_email_template(template_type)

        users = []

        link = "".join([AccountHandler.FRONT_END, '#/reviewData/', str(submission_id)])
        email_template = {'[REV_USER_NAME]': g.user.name, '[REV_AGENCY]': agency_name, '[REV_URL]': link}

        for user_id in user_ids:
            # Check if user id is valid, if so add User object to array
            users.append(sess.query(User).filter(User.user_id == user_id).one())

        for user in users:
            new_email = SesEmail(user.email, system_email, template_type=template_type, parameters=email_template)
            new_email.send()

        return JsonResponse.create(StatusCode.OK, {"message": "Emails successfully sent"})


def perms_to_affiliations(perms, user_id, service_account_flag=False):
    """ Convert a list of perms from MAX to a list of UserAffiliations. Filter out and log any malformed perms

        Args:
            perms: list of permissions (as strings) for the user
            user_id: the ID of the user
            service_account_flag: flag to indicate a service account
        Yields:
            UserAffiliations based on the permissions provided
    """
    available_cgacs = {cgac.cgac_code: cgac for cgac in GlobalDB.db().session.query(CGAC)}
    available_frecs = {frec.frec_code: frec for frec in GlobalDB.db().session.query(FREC)}
    log_data = {
        'message_type': 'BrokerWarning',
        'user_id': user_id
    }
    for perm in perms:
        log_data['message'] = 'User with ID {} has malformed permission: {}'.format(user_id, perm)
        components = perm.split('-PERM_')
        if len(components) != 2:
            logger.warning(log_data)
            continue

        codes, perm_level = components
        split_codes = codes.split('-FREC_')
        frec_code, cgac_code = None, None
        if len(split_codes) == 2:
            # permissions for FR entity code and readonly CGAC
            frec_code, cgac_code = split_codes[1], split_codes[0]
            if frec_code not in available_frecs or cgac_code not in available_cgacs:
                logger.warning(log_data)
                continue
        else:
            # permissions for CGAC
            cgac_code = codes
            if cgac_code not in available_cgacs:
                logger.warning(log_data)
                continue

        perm_level = perm_level.lower()

        if service_account_flag:
            # Replace MAX Service Account permissions with Broker "write" and "editfabs" permissions
            perm_level = 'we'
        elif perm_level not in 'rwsef':
            logger.warning(log_data)
            continue

        for permission in perm_level:
            if frec_code:
                yield UserAffiliation(
                    cgac=available_cgacs[cgac_code],
                    frec=None,
                    permission_type_id=PERMISSION_SHORT_DICT['r']
                )
                yield UserAffiliation(
                    cgac=None,
                    frec=available_frecs[frec_code],
                    permission_type_id=PERMISSION_SHORT_DICT[permission]
                )
            else:
                yield UserAffiliation(
                    cgac=available_cgacs[cgac_code] if cgac_code else None,
                    frec=None,
                    permission_type_id=PERMISSION_SHORT_DICT[permission]
                )


def best_affiliation(affiliations):
    """ If a user has multiple permissions for a single agency, select the best

        Args:
            affiliations: list of UserAffiliations a user has

        Returns:
            List of all affiliations the user has (with duplicates, highest of each type/agency provided)
    """
    dabs_dict, fabs_dict = {}, {}

    # Sort all affiliations from lowest to highest permission
    sorted_affiliations = sorted(list(affiliations), key=attrgetter('permission_type_id'))

    for affiliation in sorted_affiliations:
        # Overwrite low permissions with high permissions; keep DABS and FABS separate so FABS doesn't overwrite DABS
        if affiliation.permission_type_id in DABS_PERMISSION_ID_LIST:
            dabs_dict[affiliation.cgac, affiliation.frec] = affiliation
        elif affiliation.permission_type_id in FABS_PERMISSION_ID_LIST:
            fabs_dict[affiliation.cgac, affiliation.frec] = affiliation

    all_affils = list(dabs_dict.values()) + list(fabs_dict.values())
    return all_affils


def set_user_name(user, cas_attrs):
    """ Update the name for the user based on the MAX attributes.

        Args:
            user: the User object
            cas_attrs: a dictionary of the max attributes (includes first, middle, last names) for a logged in user
    """
    first_name = cas_attrs['maxAttribute:First-Name']
    middle_name = cas_attrs['maxAttribute:Middle-Name']
    last_name = cas_attrs['maxAttribute:Last-Name']

    # Check for None first so the condition can short-circuit without
    # having to worry about calling strip() on a None object
    if middle_name is None or middle_name.strip() == '':
        user.name = first_name + " " + last_name
    else:
        user.name = first_name + " " + middle_name[0] + ". " + last_name


def set_max_perms(user, max_group_list, service_account_flag=False):
    """ Convert the user group lists present on MAX into a list of UserAffiliations and/or website_admin status.

        Permissions are encoded as a comma-separated list of:
        {parent-group}-CGAC_{cgac-code}-PERM_{one-of-R-W-S-F}
        {parent-group}-CGAC_{cgac-code}-FREC_{frec_code}-PERM_{one-of-R-W-S-F}
        or
        {parent-group}-CGAC_SYS to indicate website_admin

        Args:
            user: the User object
            max_group_list: list of all MAX groups the user has
            service_account_flag: flag to indicate a service account
    """
    prefix = CONFIG_BROKER['parent_group'] + '-CGAC_'

    # Each group name that we care about begins with the prefix, but once we have that list, we don't need the
    # prefix anymore, so trim it off.
    perms = [group_name[len(prefix):]
             for group_name in max_group_list.split(',')
             if group_name.startswith(prefix)]

    if 'SYS' in perms:
        user.affiliations = []
        user.website_admin = True
    else:
        affiliations = best_affiliation(perms_to_affiliations(perms, user.user_id, service_account_flag))

        user.affiliations = affiliations
        user.website_admin = False


def json_for_user(user, session_id):
    """ Convert the provided user to a dictionary (for JSON)

        Args:
            user: the User object

        Returns:
            An object containing user details
    """
    return {
        "user_id": user.user_id,
        "name": user.name,
        "title": user.title,
        "skip_guide": user.skip_guide,
        "website_admin": user.website_admin,
        "affiliations": [{"agency_name": affil.cgac.agency_name, "permission": affil.permission_type_name}
                         if affil.cgac else
                         {"agency_name": affil.frec.agency_name, "permission": affil.permission_type_name}
                         for affil in user.affiliations],
        "session_id": session_id
    }


def get_max_dict(ticket, service):
    """ Get the result from MAX's serviceValidate functionality

        Args:
            ticket: the ticket to send to MAX
            service: the service to send to MAX

        Returns:
            A dictionary of the response from MAX
    """
    url = CONFIG_BROKER['cas_service_url'].format(ticket, service)
    max_xml = requests.get(url).content
    return xmltodict.parse(max_xml)


def logout(session):
    """ This function removes the session from the session table if currently logged in, and then returns a success
        message

        Args:
            session: the Session object

        Returns:
            a JsonResponse that the logout was successful
    """
    # Call session handler
    LoginSession.logout(session)
    return JsonResponse.create(StatusCode.OK, {"message": "Logout successful"})


def list_user_emails():
    """ List user names and emails

        Returns:
            A JsonResponse that contains a list of user information (ID, name, and email)
    """
    sess = GlobalDB.db().session
    users = sess.query(User)
    if not g.user.website_admin:
        relevant_cgacs = [aff.cgac_id for aff in g.user.affiliations]
        subquery = sess.query(UserAffiliation.user_id).filter(UserAffiliation.cgac_id.in_(relevant_cgacs))
        users = users.filter(User.user_id.in_(subquery))

    user_info = [{"id": user.user_id, "name": user.name, "email": user.email} for user in users]
    return JsonResponse.create(StatusCode.OK, {"users": user_info})
