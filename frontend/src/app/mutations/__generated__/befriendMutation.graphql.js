/**
 * @flow
 * @relayHash 70c8e579dad0aee4dc6b323e95496cad
 */

/* eslint-disable */

'use strict';

/*::
import type {ConcreteBatch} from 'relay-runtime';
export type befriendMutationVariables = {|
  input: {
    userId: $ReadOnlyArray<?number>;
    clientMutationId?: ?string;
  };
|};

export type befriendMutationResponse = {|
  +befriend: ?{|
    +users: ?$ReadOnlyArray<?{|
      +id: string;
      +isFriendOfMe: ?boolean;
      +isSubscribedByMe: ?boolean;
    |}>;
  |};
|};
*/


/*
mutation befriendMutation(
  $input: UserConnectionMutationInput!
) {
  befriend(input: $input) {
    users {
      id
      isFriendOfMe
      isSubscribedByMe
    }
  }
}
*/

const batch /*: ConcreteBatch*/ = {
  "fragment": {
    "argumentDefinitions": [
      {
        "kind": "LocalArgument",
        "name": "input",
        "type": "UserConnectionMutationInput!",
        "defaultValue": null
      }
    ],
    "kind": "Fragment",
    "metadata": null,
    "name": "befriendMutation",
    "selections": [
      {
        "kind": "LinkedField",
        "alias": null,
        "args": [
          {
            "kind": "Variable",
            "name": "input",
            "variableName": "input",
            "type": "UserConnectionMutationInput!"
          }
        ],
        "concreteType": "UserConnectionMutationPayload",
        "name": "befriend",
        "plural": false,
        "selections": [
          {
            "kind": "LinkedField",
            "alias": null,
            "args": null,
            "concreteType": "User",
            "name": "users",
            "plural": true,
            "selections": [
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "id",
                "storageKey": null
              },
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "isFriendOfMe",
                "storageKey": null
              },
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "isSubscribedByMe",
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ],
    "type": "Mutation"
  },
  "id": null,
  "kind": "Batch",
  "metadata": {},
  "name": "befriendMutation",
  "query": {
    "argumentDefinitions": [
      {
        "kind": "LocalArgument",
        "name": "input",
        "type": "UserConnectionMutationInput!",
        "defaultValue": null
      }
    ],
    "kind": "Root",
    "name": "befriendMutation",
    "operation": "mutation",
    "selections": [
      {
        "kind": "LinkedField",
        "alias": null,
        "args": [
          {
            "kind": "Variable",
            "name": "input",
            "variableName": "input",
            "type": "UserConnectionMutationInput!"
          }
        ],
        "concreteType": "UserConnectionMutationPayload",
        "name": "befriend",
        "plural": false,
        "selections": [
          {
            "kind": "LinkedField",
            "alias": null,
            "args": null,
            "concreteType": "User",
            "name": "users",
            "plural": true,
            "selections": [
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "id",
                "storageKey": null
              },
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "isFriendOfMe",
                "storageKey": null
              },
              {
                "kind": "ScalarField",
                "alias": null,
                "args": null,
                "name": "isSubscribedByMe",
                "storageKey": null
              }
            ],
            "storageKey": null
          }
        ],
        "storageKey": null
      }
    ]
  },
  "text": "mutation befriendMutation(\n  $input: UserConnectionMutationInput!\n) {\n  befriend(input: $input) {\n    users {\n      id\n      isFriendOfMe\n      isSubscribedByMe\n    }\n  }\n}\n"
};

module.exports = batch;
