import { addToStringArrayIfNotPresent, removeFromStringArray } from "../../utils";

function hideUserSummaryContainer(obj: WithUserSummaryContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.userSummaryContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  )
}

function initialUserSummaryContainerClasses(): Array<string> {
  return [
    "animatable",
    "container-large-centered-with-content-centered",
    "debug",
    "whitespaced-vertically"
  ]
}

function showUserSummaryContainer(obj: WithUserSummaryContainer): void {
  removeFromStringArray(obj.userSummaryContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.userSummaryContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.userSummaryContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  );
}

interface WithUserSummaryContainer {
  animationTimeout: number;
  userSummaryContainerClasses: Array<string>
}

export {
  hideUserSummaryContainer,
  initialUserSummaryContainerClasses,
  showUserSummaryContainer,
  WithUserSummaryContainer
}
