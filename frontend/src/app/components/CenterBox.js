import React from "react";

export default class CenterBox extends React.Component {
  render() {
    const { children, className = "", ...restProps } = this.props;
    return (
      <div
        {...restProps}
        className={`${className} d-flex justify-content-center align-items-center`}
      >
        {children}
      </div>
    );
  }
}
