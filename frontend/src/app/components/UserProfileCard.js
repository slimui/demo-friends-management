import React from "react";
import PropTypes from "prop-types";

export default class UserProfileCard extends React.Component {
  static propTypes = {
    user: PropTypes.object.isRequired
  };
  render() {
    const { user, className = "", ...restProps } = this.props;
    const avatarProps = {
      className: "rounded-circle mt-3 img-thumbnail",
      style: styles.avatar
    };
    const avatar = user.avatar_url ? (
      <img src={user.avatar_url} {...avatarProps} />
    ) : (
      <div {...avatarProps} />
    );
    return (
      <div {...restProps} className={`${className} card d-flex flex-column justify-content-around align-items-center`}>
        {avatar}
        <div className="card-body">
          <small className="d-block text-secondary text-center">You Are</small>
          <h4 class="card-title">
            {user.first_name} {user.last_name}
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
