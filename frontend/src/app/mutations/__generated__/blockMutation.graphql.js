/**
 * @flow
 * @relayHash b8310ee16f62c263ece29c4ee718a5f1
 */

/* eslint-disable */

'use strict';

/*::
import type {ConcreteBatch} from 'relay-runtime';
export type blockMutationVariables = {|
  input: {
    userId: $ReadOnlyArray<?number>;
    clientMutationId?: ?string;
  };
|};

export type blockMutationResponse = {|
  +block: ?{|
    +users: ?$ReadOnlyArray<?{|
      +id: string;
      +isBlockedByMe: ?boolean;
      +isSubscribedByMe: ?boolean;
    |}>;
  |};
|};
*/


/*
mutation blockMutation(
  $input: UserConnectionMutationInput!
) {
  block(input: $input) {
    users {
      id
      isBlockedByMe
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
    "name": "blockMutation",
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
        "name": "block",
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
                "name": "isBlockedByMe",
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
  "name": "blockMutation",
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
    "name": "blockMutation",
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
        "name": "block",
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
                "name": "isBlockedByMe",
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
  "text": "mutation blockMutation(\n  $input: UserConnectionMutationInput!\n) {\n  block(input: $input) {\n    users {\n      id\n      isBlockedByMe\n      isSubscribedByMe\n    }\n  }\n}\n"
};

module.exports = batch;
