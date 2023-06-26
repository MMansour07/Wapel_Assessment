using EMS.Service.Interfaces;
using System.Web.Mvc;
using System.Threading.Tasks;
using EMS.Core.Dtos.Task;
using EMS.Core.Helper;

namespace EMS.Webclient.Controllers
{
    [Authorize(Roles = ERole.HR)]
    public class TaskController : BaseController
    {
        private readonly IAuthService _authService;

        private readonly ITaskServcie _taskServcie;
        private readonly ITaskCriteriaServcie _taskCriteriaServcie;

        public TaskController(IAuthService authService, ITaskServcie taskServcie, ITaskCriteriaServcie taskCriteriaServcie)
        {
            _taskServcie = taskServcie;
            _authService = authService;
            _taskCriteriaServcie = taskCriteriaServcie;
        }


        //[OverrideAuthorization]
        //[Authorize(Roles = ERole.HR + "," + ERole.Employee)]
        [HttpGet]
        public async Task<ActionResult> New()
        {
            var usersResponse = await _authService.GetUsersAsSelectList();
            if (usersResponse.Success)
            {
                ViewBag.Users = usersResponse.Data;

                var CriteriaResponse = await _taskCriteriaServcie.GetCriterias();

                if (CriteriaResponse.Success)
                {
                    ViewBag.Criterias = CriteriaResponse.Data;
                    return View();
                }
                else
                    return RedirectToAction("Acknowledge", new { message = CriteriaResponse.Message });
            }
            return RedirectToAction("Acknowledge", new { message = usersResponse.Message });
        }

        //[OverrideAuthorization]
        //[Authorize(Roles = ERole.HR + "," + ERole.Employee)]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> New(NewTaskDto req)
        {
            if (ModelState.IsValid)
            {
                var result = await _taskServcie.CreateTaskAsync(req);
                if (result.Success)
                    return RedirectToAction("Land", "User");
                else
                    // handle failure
                    // navigate to acknowledge page
                    return RedirectToAction("Acknowledge", new { message = result.Message });
            }

            var usersResponse = await _authService.GetUsersAsSelectList();
            if (usersResponse.Success)
            {
                ViewBag.Users = usersResponse.Data;

                var CriteriaResponse = await _taskCriteriaServcie.GetCriterias();

                if (CriteriaResponse.Success)
                {
                    ViewBag.Criterias = CriteriaResponse.Data;
                    return View(req);
                }
                else
                    return RedirectToAction("Acknowledge", new { message = CriteriaResponse.Message });
            }
            return RedirectToAction("Acknowledge", new { message = usersResponse.Message });
        }

    }
}
