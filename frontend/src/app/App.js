import React from "react";
import UserColumn from "./UserColumn";
import UsersContainer from "./UsersContainer";

const PORTAL_MIN_WIDTH = 768; // small devices, landscape
const USER_COLUMN_WIDTH = 280;

export default class App extends React.Component {
  render() {
    const { store } = this.props;
    return (
      <div className="d-flex" style={styles.portal}>
        <UsersContainer
          className="border border-left-0 border-top-0 border-bottom-0"
          style={styles.usersContainer}
        />
        <UserColumn style={styles.userColumn} />
      </div>
    );
  }
}

const styles = {
  portal: {
    position: "absolute",
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    minWidth: PORTAL_MIN_WIDTH
  },
  usersContainer: {
    flex: 1
  },
  userColumn: {
    width: USER_COLUMN_WIDTH
  }
};
