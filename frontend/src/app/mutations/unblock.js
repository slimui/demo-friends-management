import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation unblockMutation($input: UserConnectionMutationInput!) {
    unblock(input: $input) {
      users {
        id
        isBlockedByMe
        isSubscribedByMe
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