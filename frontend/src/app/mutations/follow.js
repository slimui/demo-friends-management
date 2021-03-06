import { commitMutation, graphql } from "react-relay";

const mutation = graphql`
  mutation followMutation($input: UserConnectionMutationInput!) {
    follow(input: $input) {
      users {
        id
        isFollowedByMe
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
