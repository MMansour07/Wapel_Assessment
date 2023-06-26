using AutoMapper;
using EMS.Core.Model;
using EMS.Core.Dtos.User;
using EMS.Core.Dtos.UserInfo;
using System.Linq;
using EMS.Core.Dtos.Evaluation;
using EMS.Core.Dtos.General;
using Microsoft.AspNet.Identity.EntityFramework;
using EMS.Core.Dtos.UserRole;
using EMS.Core.Dtos.Role;
using EMS.Core.Dtos.Department;
using EMS.Core.Dtos.TaskCriteria;
using EMS.Core.Dtos.Task;
using EMS.Core.Dtos.Rating;

namespace EMS.Service.Infrastructure
{
    public class MappingProfile : Profile
    {
        public static IMapper Mapper { get; private set; }
        public static MapperConfiguration MapperConfiguration { get; private set; }
        public static IMapper Init()
        {
            MapperConfiguration = new MapperConfiguration(cfg =>
            {
                cfg.CreateMap<User, RegisterUserDto>().ReverseMap();
                cfg.CreateMap<User, SigninUserDto>().ReverseMap();
                cfg.CreateMap<User, UserInfoDto>().ReverseMap();
                cfg.CreateMap<User, UserEditDto>().ForMember(vm => vm.SelectedRoles, m => m.MapFrom(u => u.Roles.Select(x => x.RoleId)));
                cfg.CreateMap<UserEditDto, User>().ForMember(vm => vm.Roles, m => m.MapFrom(u => u.SelectedRoles.Select(x => new IdentityUserRole() { RoleId = x, UserId = u.Id})));
                cfg.CreateMap<User, UserDto>().ReverseMap();
                cfg.CreateMap<User, NewUserDto>().ReverseMap();
                cfg.CreateMap<Evaluation, NewEvaluationDto>().ReverseMap();
                cfg.CreateMap<IdentityUserRole, GetRoleDto>().ReverseMap();
                cfg.CreateMap<Evaluation, EditEvaluationDto>().ReverseMap();
                cfg.CreateMap<Evaluation, EditEvaluationPostDto>().ReverseMap();
                cfg.CreateMap<TaskCriteria, NewCriteriaDto>().ReverseMap();
                cfg.CreateMap<TaskCriteria, CriteriaDto>().ReverseMap();
                cfg.CreateMap<Task, NewTaskDto>().ReverseMap();
                cfg.CreateMap<Task, TaskDto>().ReverseMap();

                cfg.CreateMap<Rating, NewRatingDto>().ReverseMap();
                //cfg.CreateMap<RatingDto, Rating>();
                cfg.CreateMap<Rating, RatingDto>().ForMember(vm => vm.User, m => m.MapFrom(u => u.Task.User.FirstName + " " + u.Task.User.LastName ));
                //cfg.CreateMap<Media, MediaDto>().ReverseMap();
                cfg.CreateMap<IdentityUserRoleDto, IdentityUserRole>().ReverseMap();
                cfg.CreateMap<PagedList<Evaluation>, TableModel<EvaluationDto>>().ConvertUsing<TableModelConverter>();
                cfg.CreateMap<PagedList<User>, TableModel<UserDto>>().ConvertUsing<UserModelConverter>();
                cfg.CreateMap<Evaluation, EvaluationDto>().ReverseMap();
                //cfg.CreateMap<VideoUploadResult, Media>();
                cfg.CreateMap<RegisterUserDto, SigninUserDto>().ReverseMap();
                cfg.CreateMap<IdentityRole, RoleDto>().ReverseMap();
                cfg.CreateMap<Department, DepartmentDto>().ReverseMap();
            });
            return Mapper = MapperConfiguration.CreateMapper();
        }
    }
    public class TableModelConverter : ITypeConverter<PagedList<Evaluation>, TableModel<EvaluationDto>>
    {
        public TableModel<EvaluationDto> Convert(PagedList<Evaluation> source, TableModel<EvaluationDto> destination, ResolutionContext context)
        {
            var model = source;
            var vm = model.Select(m => MappingProfile.Mapper.Map<Evaluation, EvaluationDto>(m)).ToList();
            var data = new PagedList<EvaluationDto>(vm, model.Count, model.CurrentPage, model.PageSize, model.TotalCount);
            return new TableModel<EvaluationDto>() { meta = new Meta() { page = source.CurrentPage, pages = source.TotalPages, perpage = source.PageSize, total = source.TotalCount, totalFiltered = source.TotalCount }, data = data };
        }
    }

    public class UserModelConverter : ITypeConverter<PagedList<User>, TableModel<UserDto>>
    {
        public TableModel<UserDto> Convert(PagedList<User> source, TableModel<UserDto> destination, ResolutionContext context)
        {
            var model = source;
            var vm = model.Select(m => MappingProfile.Mapper.Map<User, UserDto>(m)).ToList();
            var data = new PagedList<UserDto>(vm, model.Count, model.CurrentPage, model.PageSize, model.TotalCount);
            return new TableModel<UserDto>() { meta = new Meta() { page = source.CurrentPage, pages = source.TotalPages, perpage = source.PageSize, total = source.TotalCount, totalFiltered = source.TotalCount }, data = data };
        }
    }
}
