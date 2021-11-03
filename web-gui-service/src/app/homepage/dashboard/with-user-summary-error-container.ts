import { addToStringArrayIfNotPresent, removeFromStringArray } from '../../utils';

function hideUserSummaryErrorContainer(obj: WithUserSummaryErrorContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryErrorContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.userSummaryErrorContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  );
}

function intialUserSummaryErrorContainerClasses(): Array<string> {
  return [
    "animated",
    "container-large-centered-with-content-centered",
    "debug",
    "whitespaced-vertically"
  ]
}

function showUserSummaryErrorContainer(obj: WithUserSummaryErrorContainer): void {
  removeFromStringArray(obj.userSummaryErrorContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.userSummaryErrorContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryErrorContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.userSummaryErrorContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  )
}

interface WithUserSummaryErrorContainer {
  animationTimeout: number,
  userSummaryErrorContainerClasses: Array<string>
}

export {
  intialUserSummaryErrorContainerClasses,
  hideUserSummaryErrorContainer,
  showUserSummaryErrorContainer,
  WithUserSummaryErrorContainer
}
