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

## Decisions made
* Django 4.2 as relatively new LTS version (till April 2026)
* Python 3.10 - relatively fresh, supported by Django 4.2 with similar EOL (October 2026)
* coverage 7.3.2, to estimate unit test coverage in PyCharm
