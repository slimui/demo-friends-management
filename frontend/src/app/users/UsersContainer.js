import React from "react";
import Spinner from "./components/Spinner";
import CenterBox from "./components/CenterBox";
import { QueryRenderer, graphql } from "react-relay";
import { inject, observer } from "mobx-react";
import UserCard from './UserCard'

const query = graphql`
  query UsersContainerQuery {
    me {
      userId
      firstName
      lastName
    }
  }
`;

@inject(["store"])
@observer
class UsersContainer extends React.Component {
  state = {
    query
  };
  _render = ({ props, error }) => {
    const { store, className = "", ...restProps } = this.props;
    let children;
    if (error) {
      children = (
        <CenterBox>
          <div className="alert alert-danger d-inline p-3" role="alert">
            Sorry, an error has occurred.
          </div>
        </CenterBox>
      );
    } else if (!props) {
      children = (
        <CenterBox>
          <Spinner visible />
        </CenterBox>
      );
    } else {
      children = <code>TODO</code>;
    }
    return (
      <div {...restProps} className={`${className} d-flex flex-column p-3`}>
        {children}
      </div>
    );
  };
  render() {
    const { store } = this.props;
    return (
      <QueryRenderer
        environment={this.props.store.environment}
        query={this.state.query}
        variables={{ meId: store.meId }}
        render={this._render}
      />
    );
  }
}

export default UsersContainer;
