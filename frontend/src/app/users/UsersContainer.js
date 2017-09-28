import React from "react";
import Spinner from "../components/Spinner";
import CenterBox from "../components/CenterBox";
import { QueryRenderer, graphql } from "react-relay";
import { inject, observer } from "mobx-react";
import UsersPagination from "./UsersPagination";

const query = graphql`
  query UsersContainerQuery($count: Int!, $cursor: String) {
    ...UsersPagination_allUsers
  }
`;

const PAGESIZE = 50;
const variables = { count: PAGESIZE, cursor: null };

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
        <CenterBox style={{ height: '100%' }}>
          <div className="alert alert-danger d-inline p-3" role="alert">
            Sorry, an error has occurred.
          </div>
        </CenterBox>
      );
    } else if (!props) {
      children = (
        <CenterBox style={{ height: '100%' }}>
          <Spinner visible />
        </CenterBox>
      );
    } else {
      children = (
        <UsersPagination allUsers={props} pageSize={PAGESIZE} store={store} />
      );
    }
    return (
      <div {...restProps} className={`${className} p-3`}>
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
        variables={variables}
        render={this._render}
      />
    );
  }
}

export default UsersContainer;
