using EMS.Service.Interfaces;
using System.Web.Mvc;
using System.Threading.Tasks;
using EMS.Core.Dtos.Rating;
using Microsoft.AspNet.Identity;
using EMS.Core.Helper;

namespace EMS.Webclient.Controllers
{
    [Authorize]
    public class RatingController : BaseController
    {
        private readonly IAuthService _authService;

        private readonly ITaskServcie _taskServcie;
        private readonly ITaskCriteriaServcie _taskCriteriaServcie;
        private readonly IRatingServcie _rateServcie;

        public RatingController(IAuthService authService, ITaskServcie taskServcie, ITaskCriteriaServcie taskCriteriaServcie, IRatingServcie rateServcie)
        {
            _taskServcie = taskServcie;
            _authService = authService;
            _taskCriteriaServcie = taskCriteriaServcie;
            _rateServcie = rateServcie;
        }


        [HttpGet]
        public ActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public async Task<ActionResult> Ratinglst()
        {
            var response = await _rateServcie.GetRatings(User.Identity.GetUserId());

            if (response.Success)
                return Json(response.Data, JsonRequestBehavior.AllowGet);
            else
                return Json(response.Data, JsonRequestBehavior.AllowGet);
            // handle failure
            // navigate to acknowledge page
        }


        [OverrideAuthorization]
        [Authorize(Roles = ERole.HR)]
        [HttpGet]
        public async Task<ActionResult> New()
        {
            var CriteriaResponse = await _taskCriteriaServcie.GetCriterias();

            if (CriteriaResponse.Success)
            {
                ViewBag.Criterias = CriteriaResponse.Data;
                return View();
            }
            else
                return RedirectToAction("Acknowledge", new { message = CriteriaResponse.Message });
        }

        [HttpGet]
        //[NonAction]
        public async Task<ActionResult> GetTasksByCritriaId(int TaskCriteridId)
        {
           var tasks = await _taskServcie.GetTasksByCriteriaId(TaskCriteridId);

            if (tasks.Success)
                return Json(tasks, JsonRequestBehavior.AllowGet);
            else
                return RedirectToAction("Acknowledge", new { message = tasks.Message });
        }



        [OverrideAuthorization]
        [Authorize(Roles = ERole.HR)]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<ActionResult> New(NewRatingDto req)
        {
            if (ModelState.IsValid)
            {
                var result = await _rateServcie.CreateRatingAsync(req);
                if (result.Success)
                    return RedirectToAction("Index");
                else
                    // handle failure
                    // navigate to acknowledge page
                    return RedirectToAction("Acknowledge", new { message = result.Message });
            }

            var CriteriaResponse = await _taskCriteriaServcie.GetCriterias();

            if (CriteriaResponse.Success)
            {
                ViewBag.Criterias = CriteriaResponse.Data;
                return View(req);
            }
            else
                return RedirectToAction("Acknowledge", new { message = CriteriaResponse.Message });

        }



        [HttpGet]
        public async Task<ActionResult> Details(int id)
        {
            var response = await _rateServcie.GetRatingInfoAsync(id);

            if (response.Success)
            {
                var CriteriaResponse = await _taskCriteriaServcie.GetCriterias();

                if (CriteriaResponse.Success)
                {
                    ViewBag.Criterias = CriteriaResponse.Data;

                    var taskResponse = await _taskServcie.GetTasksByCriteriaId(response.Data.TaskCriteriaId);

                    if (taskResponse.Success)
                    {
                        ViewBag.Tasks = taskResponse.Data;
                        return View(response.Data);
                    }
                    else
                        return RedirectToAction("Acknowledge", new { message = taskResponse.Message });
                }
                return RedirectToAction("Acknowledge", new { message = CriteriaResponse.Message });

            }
            else
                return RedirectToAction("Acknowledge", new { message = response.Message });


            // handle failure
            // navigate to acknowledge page
        }

    }
}
