namespace DatingApp.API.helpers
{
    //public class LogUserActivity : IAsyncActionFilter
    //{
    //    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    //    {
    //        var resultcontext = await next();
    //        var userId = int.Parse(resultcontext.HttpContext.User.FindFirst(ClaimTypes.NameIdentifier).Value);
    //        var repo =  resultcontext.HttpContext.RequestServices.GetService<IDatingAppRepository>();
    //        var user = await repo.GetUser(userId);
    //        user.LastActive = DateTime.Now;
    //        await repo.SaveAll();

    //    }
    //}
}