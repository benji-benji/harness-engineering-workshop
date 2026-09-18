---
name: add-resource
description: Add a new resource to the orders service, with a route, a service, a repository and a test. Use when asked to add a new resource, entity or group of endpoints.
---

# Add a resource

1. Run `python scripts/new_resource.py <name>` with a singular, lower case name such as `refund`.
2. The script creates four files, one in each of `shop/routes/`, `shop/services/`, `shop/repositories/` and `tests/`. Do not create these files by hand.
3. Fill in the repository, then the service, then the route.
4. Register the router in `shop/app.py`.
5. Run `./sensors.sh check` before you finish.