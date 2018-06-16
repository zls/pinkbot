import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "./containers/Home";
import Prepare from "./containers/Prepare";

export default () =>
  <Switch>
    <Route path="/" exact component={Home} />
    <Route path="/prepare" exact component={Prepare} />
  </Switch>;