import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation befriendMutation($input: UserConnectionMutationInput!) {
    befriend(input: $input) {
      users {
        id
        fullName
        isFriendOfMe
        isSubscribedByMe
        commonFriendsWithMe {
          id
          fullName
          avatarUrl
          commonFriendsWithMe {
            id
            fullName
            avatarUrl
          }
        }
      }
      relatedUsers {
        id
        fullName
        commonFriendsWithMe {
          id
          fullName
          avatarUrl
          commonFriendsWithMe {
            id
            fullName
            avatarUrl
          }
        }
      }
    }
  }
`;

export default (environment, userId) => {
  const variables = { input: { userId } };
  return new Promise((resolve, reject) => {
    commitMutation(environment, {
      mutation,
      variables,
      onCompleted: (resp, errors) => {
        errors ? reject(errors) : resolve(resp);
      }
    });
  });
};
