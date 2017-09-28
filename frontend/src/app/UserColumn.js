import React from "react";
import UserProfileCard from "./components/UserProfileCard";
import { inject, observer } from "mobx-react";

@inject(["store"])
@observer
class UserColumn extends React.Component {
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
        <form>
          <div className="form-group">
            <label htmlFor="input-me-id" className="text-secondary small">
              View this app as
            </label>

            <select
              id="input-me-id"
              className="form-control"
              value={store.meId}
              onChange={this.onUserSelect}
            >
              {store.users.map(user => {
                return (
                  <option key={user.user_id} value={user.user_id}>
                    {user.first_name} {user.last_name}
                  </option>
                );
              })}
            </select>
          </div>
          <hr />
          <UserProfileCard user={store.me} />
        </form>
      </div>
    );
  }
}

export default UserColumn;
