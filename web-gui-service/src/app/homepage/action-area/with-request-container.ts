import { addToStringArrayIfNotPresent, removeFromStringArray } from "src/app/utils";

function initialRequestContainerClasses(): Array<string> {
  return [
    "animated",
    "debug",
    "whitespaced-completely"
  ]
}

function hideRequestContainer(obj: WithRequestContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.requestContainerClasses, "rendered-visible");
      addToStringArrayIfNotPresent(obj.requestContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  );
}

function showRequestContainer(obj: WithRequestContainer): void {
  removeFromStringArray(obj.requestContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.requestContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.requestContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.requestContainerClasses, "rendered-visible");
    },
    obj.animationTimeout
  );
}

interface WithRequestContainer {
  animationTimeout: number;
  requestContainerClasses: Array<string>;
}

export {
  hideRequestContainer,
  initialRequestContainerClasses,
  showRequestContainer,
  WithRequestContainer
}
