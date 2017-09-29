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

const CARDSIZE = 240;
const AVATARSIZE = 64;
const AVATARSMALLSIZE = 32;
const SPACING = 6;

class UserCard extends React.Component {
  static propTypes = {
    store: PropTypes.object.isRequired,
    user: PropTypes.object
  };
  onAvatarClick = evt => {
    evt.preventDefault();
    const { user, store } = this.props;
    if (store.meId != user.userId) {
      store.become(user.userId);
    }
  };
  onFriendClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const mutation = user.isFriendOfMe ? unfriend : befriend;
    mutation(environment, [user.userId]).catch(this.handleMutationError);
  };
  onFollowClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const mutation = user.isFollowedByMe ? unfollow : follow;
    mutation(environment, [user.userId]).catch(this.handleMutationError);
  };
  onBlockClick = evt => {
    evt.preventDefault();
    const { user } = this.props;
    const environment = this.props.relay.environment;
    const mutation = user.isBlockedByMe ? unblock : block;
    mutation(environment, [user.userId]).catch(this.handleMutationError);
  };
  handleMutationError = err => {
    window.alert("Sorry, you cannot perform this action.");
  }
  render() {
    const { className = "", user, store, relay, ...restProps } = this.props;
    const disabled = store.meId == user.userId;
    const buttonClassName = "btn btn-md text-center";
    const buttonProps = {
      type: "button",
      style: { flex: 1 },
      disabled
    };
    const avatar = (
      <UserAvatar
        url={user.avatarUrl}
        border
        style={{ width: AVATARSIZE, height: AVATARSIZE }}
      />
    );
    return (
      <div
        {...restProps}
        style={{ width: CARDSIZE }}
        className={`${className} card ${disabled
          ? "border-primary"
          : user.isSubscribedByMe ? "border-success" : ""}`}
      >
        <div
          className={`d-flex align-items-center justify-content-around py-2 ${disabled
            ? "bg-primary-light"
            : user.isSubscribedByMe ? "bg-success-light" : "bg-light"}`}
        >
          {!disabled ? (
            <a href="#" onClick={this.onAvatarClick}>
              {avatar}
            </a>
          ) : (
            avatar
          )}

          <div
            className="d-flex flex-column justify-content-center"
            style={{
              width: CARDSIZE - AVATARSIZE - SPACING * 3
            }}
          >
            <h6 className="my-0 text-truncate">
              <span
                className={
                  user.isSubscribedByMe
                    ? "icon-check-circle text-success"
                    : "icon-check-circle-o text-secondary"
                }
              >
                &nbsp;
              </span>
              {user.fullName}
            </h6>
            <small className="d-inline-block text-truncate text-secondary">
              {user.address}
            </small>
          </div>
        </div>
        <ul className="list-group list-group-flush">
          <li className="list-group-item">
            <div
              className="d-flex justify-content-center"
              style={{ maxHeight: AVATARSMALLSIZE }}
            >
              {!user.commonFriendsWithMe || !user.commonFriendsWithMe.length ? (
                <small
                  className="d-block text-secondary"
                  style={{
                    height: AVATARSMALLSIZE,
                    lineHeight: `${AVATARSMALLSIZE}px`
                  }}
                >
                  {disabled ? "You" : "No common friends"}
                </small>
              ) : (
                user.commonFriendsWithMe.map(friend => {
                  return (
                    <UserAvatar
                      className="mx-1"
                      key={friend.userId}
                      url={friend.avatarUrl}
                      style={{
                        width: AVATARSMALLSIZE,
                        height: AVATARSMALLSIZE
                      }}
                    />
                  );
                })
              )}{" "}
            </div>
          </li>
        </ul>
        <div className="d-flex" role="group" aria-label="Friends controls">
          <button
            {...buttonProps}
            onClick={this.onFriendClick}
            className={`${buttonClassName} ${user.isFriendOfMe
              ? "btn-drawer-primary"
              : "btn-drawer-secondary"}`}
          >
            <span className="icon-user-add">&nbsp;</span>
            <br />
            <small>Friend</small>
          </button>
          <button
            {...buttonProps}
            onClick={this.onFollowClick}
            className={`${buttonClassName} ${user.isFollowedByMe
              ? "btn-drawer-primary"
              : "btn-drawer-secondary"}`}
          >
            <span className="icon-rss">&nbsp;</span>
            <br />
            <small>Follow</small>
          </button>
          <button
            {...buttonProps}
            onClick={this.onBlockClick}
            className={`${buttonClassName} ${user.isBlockedByMe
              ? "btn-drawer-primary"
              : "btn-drawer-secondary"}`}
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
      fullName
      address
      avatarUrl
      isFriendOfMe
      isFollowedByMe
      isBlockedByMe
      isSubscribedByMe
      commonFriendsWithMe {
        id
        userId
        fullName
        avatarUrl
      }
    }
  `
);
