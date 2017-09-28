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
      return this.users.find(user => (user.userId == this.meId));
    }
    return null;
  }

  @action.bound
  initialize(users) {
    this.users = users || [];
    if (this.users.length) {
      const me = users.find(user => user.active);
      this.meId = me ? me.userId : users[0].userId;
    }
  }

  @action.bound
  become(userId) {
    this.meId = userId;
  }
}
