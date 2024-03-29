# dtt
Django Test Task

Repo created: 2023-11-20

## Requirements
### Models
* Blog article - should contain title, slug (prepopulated from title), content, author (FK to User), publication datetime, switch to make it online/offline.
* Contact request - should contain email, name, content and date. This model must be added to admin without possibility to edit fields. Only removal should be possible.

### Admin
* Article model must be registered to admin with possibility to edit all fields.
* Contact request model must be added to admin without possibility to add or edit. Only removal should be possible.
* 
### Views
* All views should be written as class-based views.
* Article list view - display 5 entries on one page with link to a detail view. Pagination links should be located at the bottom of the list.
* Article detail view - should contain slug and id in the url, display article details (title, content, full name of the author, publication datetime) and link to articles list.
* Contact view - should display form with email, name, and content. After pressing "send" button it should store the entry in the database and send an email to test@test.com with content, name and add email address as "Reply-to".

## Tech notes
* Unit test coverage
* DB - sqlite
* git
* Project should be hosted somewhere, admin is reachable
* Design is not a priority

## Development notes
* Django 4.2 as relatively new LTS version (till April 2026)
* Python 3.10 - relatively fresh, supported by Django 4.2 with similar EOL (October 2026)
* coverage 7.3.2, to estimate unit test coverage in PyCharm (current coverage - 80-100%, depending on modules)
* Deployment to AWS, to a single EC2 instance with running docker-compose
* App served in production with gunicorn app server, with nginx as a proxy
* Commits history was kept for dev branch
* Email service is live and uses MailTrap servers for testing purposes: messages are sent to the address specified in DEFAULT_TO_EMAIL setting, but is intercepted by MailTrap and not sent to the real address
* GitHub Actions are used for CI/CD, with 2 workflows: one for testing, another for deployment to AWS
* Secrets are managed with GitHub Secrets, and are used in GitHub Actions workflows
* Secrets are passed to the app with environment variables, and are used in settings.py
* CI pipeline triggers automatically on push/pull request to main branch
* CD pipeline triggered manually and required to provide EC2 instance public IP address as a parameter
