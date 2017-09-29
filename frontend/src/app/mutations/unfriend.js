import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation unfriendMutation($input: UserConnectionMutationInput!) {
    unfriend(input: $input) {
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
    }
  }
`;

export default (environment, userId) => {
  const variables = { input: { userId } };
  return new Promise((onCompleted, onError) => {
    commitMutation(environment, { mutation, variables, onCompleted, onError });
  });
};
