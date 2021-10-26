import { removeFromStringArray } from '../../utils'

function hideUserSummaryErrorContainer(obj: WithUserSummaryErrorContainer): void {
  removeFromStringArray(obj.userSummaryErrorContainerClasses, "rendered-visible");
  obj.userSummaryErrorContainerClasses.push("non-visible-non-rendered");
}

function intialUserSummaryErrorContainerClasses(): Array<string> {
  return [
    "animated",
    "container-large-centered-with-content-centered",
    "debug",
    "non-visible-non-rendered",
    "whitespaced-vertically"
  ]
}

function showUserSummaryErrorContainer(obj: WithUserSummaryErrorContainer): void {
  removeFromStringArray(obj.userSummaryErrorContainerClasses, "non-visible-non-rendered");
  obj.userSummaryErrorContainerClasses.push("non-visible-rendered");
  setTimeout(
    () => {
      removeFromStringArray(obj.userSummaryErrorContainerClasses, "non-visible-rendered");
      obj.userSummaryErrorContainerClasses.push("rendered-visible");
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
