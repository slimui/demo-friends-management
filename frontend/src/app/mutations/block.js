import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation blockMutation($input: UserConnectionMutationInput!) {
    block(input: $input) {
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
