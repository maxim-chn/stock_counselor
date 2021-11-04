import { addToStringArrayIfNotPresent, removeFromStringArray} from "src/app/utils";

function hideResponseContainer(obj: WithResponseContainer): void {
  setTimeout(
    () => {
      removeFromStringArray(obj.responseContainerClasses, "rendered-visible"),
      addToStringArrayIfNotPresent(obj.responseContainerClasses, "non-visible-non-rendered");
    },
    obj.animationTimeout
  )
}

function initialResponseContainerClasses(): Array<string> {
  return [
    "animated",
    "debug",
    "whitespaced-completely"
  ]
}

function showResponseContainer(obj: WithResponseContainer): void {
  removeFromStringArray(obj.responseContainerClasses, "non-visible-non-rendered");
  addToStringArrayIfNotPresent(obj.responseContainerClasses, "non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.responseContainerClasses, "non-visible-rendered");
      addToStringArrayIfNotPresent(obj.responseContainerClasses, "rendered-visible");
    }
  );
}

interface WithResponseContainer {
  animationTimeout: number;
  responseContainerClasses: Array<string>;
}

export {
  hideResponseContainer,
  initialResponseContainerClasses,
  showResponseContainer,
  WithResponseContainer
}
