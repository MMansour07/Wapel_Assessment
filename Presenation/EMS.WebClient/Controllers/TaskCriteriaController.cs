using EMS.Core.Helper;
using EMS.Service.Interfaces;
using System.Web.Mvc;
using EMS.Core.Dtos.TaskCriteria;
using System.Threading.Tasks;

namespace EMS.Webclient.Controllers
{
    [Authorize(Roles = ERole.HR)]
    public class TaskCriteriaController : BaseController
    {
        private readonly ITaskCriteriaServcie _taskCriteriaServcie;

        public TaskCriteriaController(ITaskCriteriaServcie taskCriteriaServcie)
        {
            _taskCriteriaServcie = taskCriteriaServcie;
        }


        [HttpGet]
        public ActionResult New()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> New(NewCriteriaDto req)
        {
            if (ModelState.IsValid)
            {
                var result = await _taskCriteriaServcie.CreateCriteriaAsync(req);
                if (result.Success)
                    return RedirectToAction("Land", "User");
                else
                    // handle failure
                    // navigate to acknowledge page
                    return RedirectToAction("Acknowledge", new { message = result.Message });
            }
            return View(req);
        }

    }
}
