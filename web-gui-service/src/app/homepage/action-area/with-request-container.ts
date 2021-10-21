import { removeFromStringArray } from "src/app/utils";

function initialRequestContainerClasses(): Array<string> {
  return [
    "animated",
    "non-visible-non-rendered"
  ]
}

function hideRequestContainer(obj: WithRequestContainer): void {
  removeFromStringArray(obj.requestContainerClasses, "rendered-visible");
  obj.requestContainerClasses.push("non-visible-non-rendered");
}

function showRequestContainer(obj: WithRequestContainer): void {
  removeFromStringArray(obj.requestContainerClasses, "non-visible-non-rendered");
  obj.requestContainerClasses.push("non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.requestContainerClasses, "non-visible-rendered");
      obj.requestContainerClasses.push("rendered-visible");
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
