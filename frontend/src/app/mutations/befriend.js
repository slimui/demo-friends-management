import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation befriendMutation($input: UserConnectionMutationInput!) {
    befriend(input: $input) {
      users {
        id
        isFriendOfMe
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
