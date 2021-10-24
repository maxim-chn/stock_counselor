import { removeFromStringArray } from "../../utils";

function hideUserSummaryContainer(obj: WithUserSummaryContainer): void {
  removeFromStringArray(obj.userSummaryContainerClasses, "rendered-visible");
  obj.userSummaryContainerClasses.push("non-visible-non-rendered");
}

function initialUserSummaryContainerClasses(): Array<string> {
  return [
    "animatable",
    "centered-horizontally",
    "non-visible-non-rendered"
  ]
}

function showUserSummaryContainer(obj: WithUserSummaryContainer): void {
  removeFromStringArray(obj.userSummaryContainerClasses, "non-visible-non-rendered");
  obj.userSummaryContainerClasses.push("non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryContainerClasses, "non-visible-rendered");
      obj.userSummaryContainerClasses.push("rendered-visible");
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
