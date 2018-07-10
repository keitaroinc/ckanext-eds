## User Roles
ckanext-eds augments CKAN's default RBAC (role based access control) with additional roles.
These roles can be set by `POST`'ing the following body to `/user_roles_create`:

```
{
  "user_id": "84b2242c-2127-4b23-91e5-3d6acc53e28f",
  "role": "editor"
}
```

`user_id` should contain the ID of the user to whom a role should be added.

`role` should contain a string representation of the role.

role can be any string value. While the original idea was to just have a editor role, the
code is written to allow for other roles aswell.

Currently, the ckanext-calendar and ckanext-pages (our own fork, not the upstream) have
integrated checks for a "editor" role, to give the ability to create, edit and delete news
and pages.
