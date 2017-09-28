import React from "react";
import { inject, observer } from "mobx-react";

@inject(["store"])
@observer
class MainColumn extends React.Component {
  render() {
    const { store, className = "", ...restProps } = this.props;
    return (
      <div
        {...restProps}
        className={`${className} d-flex flex-column p-3`}
      >
        side column
      </div>
    );
  }
}

export default MainColumn;
