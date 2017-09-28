import React from "react";
import PropTypes from "prop-types";
import { createFragmentContainer, graphql } from "react-relay";

class UserCard extends React.Component {
  static propTypes = {
    store: PropTypes.object.isRequired,
    user: PropTypes.object
  };
  render() {
    const { user } = this.props;
    return <div>{user.firstName}</div>;
  }
}

export default createFragmentContainer(
  UserCard,
  graphql`
  fragment UserCard_user on User {
    id
    userId
    firstName
  }`
);
