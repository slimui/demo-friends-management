import React from "react";

export default class CenterBox extends React.Component {
  render() {
    const { children } = this.props;
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ flex: 1 }}
      >
        {children}
      </div>
    );
  }
}
