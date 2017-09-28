/**
 * @flow
 * @relayHash 898008ff07828bd530140744d9b73c13
 */

/* eslint-disable */

'use strict';

/*::
import type {ConcreteBatch} from 'relay-runtime';
export type unfriendMutationVariables = {|
  input: {
    userId: $ReadOnlyArray<?number>;
    clientMutationId?: ?string;
  };
|};

export type unfriendMutationResponse = {|
  +unfriend: ?{|
    +users: ?$ReadOnlyArray<?{|
      +id: string;
      +isFriendOfMe: ?boolean;
      +isSubscribedByMe: ?boolean;
    |}>;
  |};
|};
*/


/*
mutation unfriendMutation(
  $input: UserConnectionMutationInput!
) {
  unfriend(input: $input) {
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
    "name": "unfriendMutation",
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
        "name": "unfriend",
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
  "name": "unfriendMutation",
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
    "name": "unfriendMutation",
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
        "name": "unfriend",
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
  "text": "mutation unfriendMutation(\n  $input: UserConnectionMutationInput!\n) {\n  unfriend(input: $input) {\n    users {\n      id\n      isFriendOfMe\n      isSubscribedByMe\n    }\n  }\n}\n"
};

module.exports = batch;
