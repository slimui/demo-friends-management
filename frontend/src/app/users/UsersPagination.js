import React from "react";
import PropTypes from "prop-types";
import CenterBox from "../components/CenterBox";
import Spinner from "../components/Spinner";
import { createPaginationContainer, graphql } from "react-relay";
import UserCard from "./UserCard";
import { debounce } from "lodash";

class UsersPagination extends React.Component {
  static propTypes = {
    store: PropTypes.object.isRequired
  };
  setRef = ref => {
    if (!ref && this.ref) {
      this.ref.parentNode.removeEventListener(
        "scroll",
        this.handleParentScroll
      );
      this.ref = null;
    } else if (ref && !this.ref) {
      this.ref = ref;
      this.ref.parentNode.addEventListener("scroll", this.handleParentScroll);
    }
  };
  handleParentScroll = debounce(evt => {
    if (!this.ref) return;
    const bounds = this.ref.getBoundingClientRect();
    const parentHeight = this.ref.parentNode.getBoundingClientRect().height;
    if (parentHeight - bounds.bottom >= 0) {
      this.loadMore();
    }
  }, 600);
  loadMore = () => {
    const { relay, pageSize } = this.props;
    if (!relay.hasMore() || relay.isLoading()) {
      return;
    }
    relay.loadMore(pageSize, err => {});
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
        ref={this.setRef}
      >
        {users.edges.map(edge => {
          return (
            <UserCard
              user={edge.node}
              key={edge.node.id}
              store={store}
              className="mb-4"
            />
          );
        })}
        <CenterBox className="mt-2 mb-3" style={{ width: "100%" }}>
          {relay.hasMore() ? (
            <Spinner visible />
          ) : (
            <small className="text-secondary">End of results</small>
          )}
        </CenterBox>
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
