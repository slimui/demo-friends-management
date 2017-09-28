import React from "react";
import ReactDOM from "react-dom";
import App from "./app/App";
import $ from "jquery";
import { Provider } from "mobx-react";
import { Store } from "./app/store";

const APPLICATION_ID = "application";

const store = new Store();

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
