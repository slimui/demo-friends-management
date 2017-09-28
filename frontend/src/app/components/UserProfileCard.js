import React from "react";
import PropTypes from "prop-types";
import UserAvatar from "./UserAvatar";

export default class UserProfileCard extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired
  };
  render() {
    const { user, className = "", ...restProps } = this.props;
    return (
      <div
        {...restProps}
        className={`${className} card d-flex flex-column justify-content-around align-items-center`}
      >
        <UserAvatar url={user.avatarUrl} />
        <div className="card-body">
          <small className="d-block text-secondary text-center">You Are</small>
          <h4 className="card-title">
            {user.fullName}
          </h4>
        </div>
      </div>
    );
  }
}

const styles = {
  avatar: {
    width: 128,
    height: 128
  }
};
