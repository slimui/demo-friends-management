import React from "react";
import { inject, observer } from "mobx-react";

@inject(["store"])
@observer
class App extends React.Component {
  render() {
    const { store } = this.props;
    return (
      <code>TODO</code>
    );
  }
}

export default App;
