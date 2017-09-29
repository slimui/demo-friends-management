import React from "react";
import PropTypes from "prop-types";

export default class UserAvatar extends React.Component {
  static propTypes = {
    url: PropTypes.string,
    border: PropTypes.bool
  };
  render() {
    const { url, className = "", border, ...restProps } = this.props;
    const avatarProps = {
      className: `${className} rounded-circle ${border
        ? "img-thumbnail"
        : ""} avatar`,
      ...restProps
    };
    return url ? <img src={url} {...avatarProps} /> : <div {...avatarProps} />;
  }
}
