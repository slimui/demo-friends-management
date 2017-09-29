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
        <div className="card d-flex flex-column justify-content-around align-items-center">
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
      </div>
    );
  }
}

export default SideColumn;
