/**
 * @flow
 * @relayHash fd265a3acc946ddec67b865a0ecd6591
 */

/* eslint-disable */

'use strict';

/*::
import type {ConcreteBatch} from 'relay-runtime';
export type unfollowMutationVariables = {|
  input: {
    userId: $ReadOnlyArray<?number>;
    clientMutationId?: ?string;
  };
|};

export type unfollowMutationResponse = {|
  +unfollow: ?{|
    +users: ?$ReadOnlyArray<?{|
      +id: string;
      +isFollowedByMe: ?boolean;
      +isSubscribedByMe: ?boolean;
    |}>;
  |};
|};
*/


/*
mutation unfollowMutation(
  $input: UserConnectionMutationInput!
) {
  unfollow(input: $input) {
    users {
      id
      isFollowedByMe
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
    "name": "unfollowMutation",
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
        "name": "unfollow",
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
                "name": "isFollowedByMe",
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
  "name": "unfollowMutation",
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
    "name": "unfollowMutation",
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
        "name": "unfollow",
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
                "name": "isFollowedByMe",
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
  "text": "mutation unfollowMutation(\n  $input: UserConnectionMutationInput!\n) {\n  unfollow(input: $input) {\n    users {\n      id\n      isFollowedByMe\n      isSubscribedByMe\n    }\n  }\n}\n"
};

module.exports = batch;
