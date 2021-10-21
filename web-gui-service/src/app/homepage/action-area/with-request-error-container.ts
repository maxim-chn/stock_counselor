import { removeFromStringArray } from "src/app/utils";

function initialRequestErrorContainerClasses(): Array<string> {
  return [
    "animated",
    "non-visible-non-rendered"
  ]
}

function hideRequestErrorContainer(obj: WithRequestErrorContainer): void {
  removeFromStringArray(obj.requestErrorContainerClasses, "rendered-visible");
  obj.requestErrorContainerClasses.push("non-visible-non-rendered");
}

function showRequestErrorContainer(obj: WithRequestErrorContainer): void {
  removeFromStringArray(obj.requestErrorContainerClasses, "non-visible-non-rendered");
  obj.requestErrorContainerClasses.push("non-visible-rendered");
    setTimeout(
      () => {
        removeFromStringArray(obj.requestErrorContainerClasses, "non-visible-rendered");
        obj.requestErrorContainerClasses.push("rendered-visible");
      },
      obj.animationTimeout
    );
}

interface WithRequestErrorContainer {
  animationTimeout: number;
  requestErrorContainerClasses: Array<string>;
}

export {
  hideRequestErrorContainer,
  initialRequestErrorContainerClasses,
  showRequestErrorContainer,
  WithRequestErrorContainer
}
