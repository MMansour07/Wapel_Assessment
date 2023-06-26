using EMS.Core.Dtos.General;
using System.Web.Mvc;

namespace EMS.Webclient.Controllers
{
    public class BaseController : Controller
    {

        //In ASP.NET MVC we have a larger list of ways to handle exception such as:

        //Try-catch-finally
        //Overriding OnException method
        //Using the[HandleError] attribute on actions and controllers
        //Setting a global exception handling filter
        //Handling Application_Error event
        //Extending HandleErrorAttribute

        // GET: Base
        [HttpGet]
        public ActionResult Acknowledge(string message)
        {
            return View(new ErrorDto() { Message = message});
        }

        [HttpGet]

        public ActionResult ErrorLogger()
        {
            return View();
        }


        //Error Handler ==> inner most after try and catch and exception filter
        protected override void OnException(ExceptionContext filterContext)
        {
            if (filterContext.ExceptionHandled)
                return;
            
            var model = new HandleErrorInfo(filterContext.Exception, filterContext.RouteData.Values["controller"].ToString(),
                filterContext.RouteData.Values["action"].ToString());
            filterContext.Result = new ViewResult()
            {
                ViewName = "ErrorLogger",
                ViewData = new ViewDataDictionary(model)
            };

            filterContext.ExceptionHandled = true;
        }
    }
}