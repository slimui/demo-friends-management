import React from "react";
import PropTypes from "prop-types";
import Spinner from "../components/Spinner";
import { createPaginationContainer, graphql } from "react-relay";
import UserCard from "./UserCard";

class UsersPagination extends React.Component {
  static propTypes = {
    store: PropTypes.object.isRequired
  };
  loadMore = () => {
    const { relay, pageSize } = this.props;
    if (!relay.hasMore() || relay.isLoading()) {
      return;
    }
    relay.loadMore(pageSize, console.log);
  };
  render() {
    const {
      className = "",
      allUsers,
      store,
      pageSize,
      relay,
      ...restProps
    } = this.props;
    const users = allUsers && allUsers.allUsers;
    if (!users || !users.edges.length) {
      return <code>EMPTY</code>;
    }
    return (
      <div
        {...restProps}
        className={`${className} d-flex flex-wrap justify-content-around`}
      >
        {users.edges.map(edge => {
          return (
            <UserCard
              user={edge.node}
              key={edge.node.id}
              store={store}
              className="mb-4"
              style={{ width: "16em" }}
            />
          );
        })}
      </div>
    );
  }
}

export default createPaginationContainer(
  UsersPagination,
  graphql`
    fragment UsersPagination_allUsers on Query {
      allUsers(first: $count, after: $cursor)
        @connection(key: "UsersPagination_allUsers") {
        edges {
          node {
            id
            ...UserCard_user
          }
        }
      }
    }
  `,
  {
    direction: "forward",
    getFragmentVariables(prevVars, totalCount) {
      return { ...prevVars, count: totalCount };
    },
    getVariables(props, { count, cursor }, fragmentVariables) {
      return { count, cursor };
    },
    query: graphql`
      query UsersPaginationQuery($count: Int!, $cursor: String) {
        ...UsersPagination_allUsers
      }
    `
  }
);
