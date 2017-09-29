import React from "react";
import UserAvatar from "./components/UserAvatar";
import { inject, observer } from "mobx-react";

@inject(["store"])
@observer
class SideColumn extends React.Component {
  onUserSelect = evt => {
    const userId = Number(evt.target.value);
    if (!userId || isNaN(userId)) {
      return;
    }
    this.props.store.become(userId);
  };
  render() {
    const { store, className = "", ...restProps } = this.props;
    const disabled = false;
    return (
      <div
        {...restProps}
        className={`${className} d-flex flex-column bg-light p-3`}
      >
        <div className="card d-flex flex-column justify-content-around align-items-center mb-3">
          <UserAvatar url={store.me.avatarUrl} className="mt-3" border />
          <div className="card-body text-center p-2">
            <p className="mb-1">
              <small className="text-secondary">View as User</small>
            </p>
            <select
              id="input-me-id"
              className="form-control mb-2"
              value={store.meId}
              onChange={this.onUserSelect}
            >
              {store.users.map(user => {
                return (
                  <option key={user.userId} value={user.userId}>
                    {user.fullName}
                  </option>
                );
              })}
            </select>
          </div>
        </div>
        <div className="small">
          <p>
            You are currently viewing this app as{" "}
            <strong>{store.me.fullName}</strong>. Click on the avatar to switch
            identity.
          </p>
          <p>
            An active <span className="icon-check-circle text-success">&nbsp;</span> subscription state means you will receive
            updates from the user in your news feeds. This is based on the
            following rules:
          </p>
          <ul className="list-unstyled">
            <li>You have not blocked the user</li>
            <li>
              You have at least on of the following:
              <ul>
                <li> Are friend of the user</li>
                <li>Followed the user</li>
              </ul>
            </li>
          </ul>
          <p>
            Whenever you befriend or unfriend a user, you will alter the
            connections between you, the user and your common friends. Try it,
            and see the changes in your common friends.
          </p>
        </div>
      </div>
    );
  }
}

export default SideColumn;
