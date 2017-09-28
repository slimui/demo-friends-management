import React from "react";
import ReactDOM from "react-dom";
import App from "./app/App";
import { Environment, Network, RecordSource, Store } from "relay-runtime";
import $ from "jquery";
import { Provider } from "mobx-react";
import { Store as AppStore } from "./app/store";

const APPLICATION_ID = "application";

const store = new AppStore();

// eslint-disable-next-line no-unused-vars
const fetchQuery = (operation, variables, cacheConfig, uploadables) => {
  return fetch("/graphql", {
    method: "POST",
    headers: {
      // We inject the 'current user' id into the request header
      // so as to emulate an authenticated user, otherwise
      // this would usually be set as server side cookie for the
      // authenticated user.
      "x-app-current-user-id": store.meId || 0,
      "content-type": "application/json"
    },
    body: JSON.stringify({
      query: operation.text, // GraphQL text from input
      variables
    })
  }).then(response => {
    return response.json();
  });
};

const createEnvironment = () => {
  const source = new RecordSource();
  const store = new Store(source);
  const network = Network.create(fetchQuery);
  return new Environment({ network, store });
};

store.environment = createEnvironment();

const render = Component => {
  ReactDOM.render(
    <Provider store={store}>
      <Component />
    </Provider>,
    document.getElementById(APPLICATION_ID)
  );
};

$(() => {
  // eslint-disable-next-line
  if (window.__users__) {
    store.initialize(window.__users__);
  }
  render(App);
});

if (module.hot) {
  module.hot.accept("./app/App", () => render(App));
}
