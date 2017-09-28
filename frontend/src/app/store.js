import { observable, action, useStrict, computed, runInAction } from "mobx";
import invariant from "invariant";

useStrict(true);

export class Store {

  /**
   * Relay environment
   */
  environment = null;

  @observable users = [];

  /**
   * Current user id
   * @type {Number}
   */
  @observable meId = null;

  @computed
  get me() {
    if (this.meId && this.users) {
      return this.users.find(user => (user.user_id == this.meId));
    }
    return null;
  }

  @action.bound
  initialize(users) {
    this.users = users || [];
    if (this.users.length) {
      const me = users.find(user => user.active);
      this.meId = me ? me.user_id : users[0].user_id;
    }
  }

  @action.bound
  become(userId) {
    this.meId = userId;
  }
}
