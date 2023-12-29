// @ts-nocheck
import React from 'react';
import { ApplyPluginsType } from '/Users/xiabo/SoftwareTest/CarbonPy/QualityDriver/frontend/node_modules/umi/node_modules/@umijs/runtime';
import * as umiExports from './umiExports';
import { plugin } from './plugin';

export function getRoutes() {
  const routes = [
  {
    "exact": true,
    "path": "/",
    "component": require('/Users/xiabo/SoftwareTest/CarbonPy/QualityDriver/frontend/src/pages/login').default
  },
  {
    "exact": true,
    "path": "/home",
    "compenent": "./home"
  },
  {
    "path": "/*",
    "redirect": "/",
    "exact": true
  }
];

  // allow user to extend routes
  plugin.applyPlugins({
    key: 'patchRoutes',
    type: ApplyPluginsType.event,
    args: { routes },
  });

  return routes;
}
