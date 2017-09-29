## Friends Management Demo

A "Friends Management" application typically found in a social network. Build with React ⚛ + GraphQL ☸ + Python 🐍.

### Goal

> For any application with a need to build its own social network, "Friends Management" is a common requirement which usually starts off simple but can grow in complexity depending on the application's use case.
>
> Usually, applications would start with features like "Friend", "Unfriend", "Block", "Receive Updates" etc.

The original exercise describes a series of REST API to provide features like:
 - Establishing a friend connection (befriend/unfriend)
 - Allowing users to follow/unfollow other users
 - Fetching friends (and followers)
 - Fetching common friends
 - Block/unblock users
 - Fetching a list of users whom an individual (aka subscriber) will subscribe to for (feed) updates, base on the following rules:
   - The subscriber has not blocked the user
   - The subscriber has at least one of the following:
     - Is a friend of the user
     - Is a follower of the user
     - ~~has `@mention` the user~~ (this was not included in the project as it is unclear what `@mention` constitutes)

### Instructions

The easiest way to run this project is to start it locally using Docker.

Install and start Docker via command line.

```
$ docker-machine start
$ eval $(docker-machine env)
```

Take note of the IP address which docker machine runs in (you'll need it later).

```
$ docker-machine ip
```

Checkout this project and start the Docker containers.

```
$ cd demo-friends-management
$ docker-compose build
$ docker-compose up -d
```

The project will run the following containers:

 - `frontend`: Runs a webpack dev server with hot-reload enabled
 - `server`: Runs a python flask server with hot-reload enabled
 - `database`: Runs a PostgreSQL server. To access the database, use `docker-compose exec database psql -U app`

This will setup a development environment for the project locally. To view the project in the browser, you'll need the Docker IP and access it at port `8000`, example `http://[docker-machine-ip]:8000/`

This project also provides a GraphQL browser at `http://[docker-machine-ip]:8000/graphql`.

To stop the project, use

```
$ docker-compose down
```

### Design Consideration

While the project requirements are quite straight forward, things get really complex when working with a social graph, where nodes (individual actors, people, things within the network) have relationships and connections (edges, links) with each other. Conventional web architecture will soon hit a roadblock as project requirements evolves and relationships become more sophisticated.

For example, a typical fetch friends api like `/api/user/[id]/friends` will soon become a bottleneck when the UI needs to:
- Show friends and **friends of friends**
- Show a list of users and **common friends** with the current user
- Show a list of users and list their **common interest**, like places visited, liked page or joined group
- When an action changes a relationship (e.g. friendships) that requires an update of the connections between multiple actors

**This will result in either a waterfall of network request (1 + n problem) or an explosion of API endpoints, not to mention the complexity to sync the UI state with the backend state.**

For this reason, I've chose to adopt [GraphQL](http://graphql.org) to power the API architecture. By providing a dynamic query based API, we can solve problems that are apparent in a social network-like application.

#### Backend Architecture

This project uses [Graphene](http://graphene-python.org) implementation of GraphQL, together with [SQLAlchemy](https://www.sqlalchemy.org) to provide SQL access interface to the backend PostgresSQL database.

- One single GraphQL endpoint for all data queries
- No more endpoint versioning, there will forever be **ONE** version, i.e. the current version
- Tooling for rapid testing and developing API endpoint ([GraphiQL](https://github.com/graphql/graphiql))
- Self documenting API endpoints

This project also apply some optimisation techniques like [DataLoader](http://docs.graphene-python.org/en/latest/execution/dataloader/) as a fetching layer to provide a consistent and highly optimised data access to the backend database. This allows us to perform batch fetching of data without sacrificing code flow and clarity. This effectively work around the n+1 fetching problem.

#### Frontend Architecture

This project leverages React + [Relay](https://facebook.github.io/relay/docs/relay-modern.html) to build the UI layer.

Relay provides us many benefits:

- Decide what data you need using GraphQL query language **when** you code the UI
- Co-locate the data access within the Views for clarity and agility
- Test and tune the data access right in the browser
- Plays nice with React's declarative nature
- No need to duplicate backend logic to maintain complex graph
- Batch querying, caching, data consistency, optimistic updates comes built-in
- Supports subscription (e.g. live updates) and persisted queries for future needs

### Others

This project was developed under time constrain, and is not bug-free and requires much UI polish. Please use issues for suggestions and bug reports.
