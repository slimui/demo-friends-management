import React from "react";
import PropTypes from "prop-types";
import UserAvatar from "../components/UserAvatar";
import { createFragmentContainer, graphql } from "react-relay";
import befriend from "../mutations/befriend";
import unfriend from "../mutations/unfriend";
import block from "../mutations/block";
import unblock from "../mutations/unblock";
import follow from "../mutations/follow";
import unfollow from "../mutations/unfollow";

const AVATARSIZE = 64;

class UserCard extends React.Component {
  static propTypes = {
    store: PropTypes.object.isRequired,
    user: PropTypes.object
  };
  onFriendClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const userId = [user.userId];
    if (user.isFriendOfMe) {
      unfriend(environment, userId);
    } else {
      befriend(environment, userId);
    }
  };
  onFollowClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const userId = [user.userId];
    if (user.isFollowedByMe) {
      unfollow(environment, userId);
    } else {
      follow(environment, userId);
    }
  };
  onBlockClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const userId = [user.userId];
    if (user.isBlockedByMe) {
      unblock(environment, userId);
    } else {
      block(environment, userId);
    }
  };
  render() {
    const { className = "", user, store, relay, ...restProps } = this.props;
    const buttonClassName = "btn btn-md text-center border-0";
    const buttonProps = {
      type: "button",
      style: { flex: 1 }
    };
    return (
      <div {...restProps} className={`${className} card`}>
        <div className="media p-3 bg-light border border-top-0 border-left-0 border-right-0">
          <UserAvatar
            url={user.avatarUrl}
            className="d-flex mr-3 align-self-center"
            style={{ width: AVATARSIZE, height: AVATARSIZE }}
          />
          <div className="media-body align-self-center">
            <h6 className="mt-0">
              <span
                className={
                  user.isSubscribedByMe
                    ? "icon-android-cloud-done text-success"
                    : "icon-android-cloud text-secondary"
                }
              >
                &nbsp;
              </span>
              {user.firstName} {user.lastName}
              <br />
              <small className="text-secondary">{user.address}</small>
            </h6>
          </div>
        </div>
        <div className="d-flex" role="group" aria-label="Friends controls">
          <button
            {...buttonProps}
            onClick={this.onFriendClick}
            className={`${buttonClassName} ${user.isFriendOfMe
              ? "btn-outline-primary"
              : "btn-outline-secondary"}`}
          >
            <span className="icon-user-add">&nbsp;</span>
            <br />
            <small>Friend</small>
          </button>
          <button
            {...buttonProps}
            onClick={this.onFollowClick}
            className={`${buttonClassName} ${user.isFollowedByMe
              ? "btn-outline-primary"
              : "btn-outline-secondary"}`}
          >
            <span className="icon-rss">&nbsp;</span>
            <br />
            <small>Follow</small>
          </button>
          <button
            {...buttonProps}
            onClick={this.onBlockClick}
            className={`${buttonClassName} ${user.isBlockedByMe
              ? "btn-outline-primary"
              : "btn-outline-secondary"}`}
          >
            <span className="icon-ban">&nbsp;</span>
            <br />
            <small>Block</small>
          </button>
        </div>
      </div>
    );
  }
}

export default createFragmentContainer(
  UserCard,
  graphql`
    fragment UserCard_user on User {
      id
      userId
      firstName
      address
      avatarUrl
      isFriendOfMe
      isFollowingMe
      isFollowedByMe
      isBlockedByMe
      isSubscribedByMe
    }
  `
);
