program gra
implicit none
integer i,j,k,nx,ny,nz,nv
real dx,dy,dz,lx,ly,lz
real potx1,potx2,poty1,poty2,potz1,potz2
real::pz1,pz2,px1,px2,py1,py2,ec1,ec2,ec3,pend,ind,capa
!Parameter(nx=150, ny=109, nz=109)
real,allocatable,DIMENSION (:)::x
real,allocatable,DIMENSION (:)::y
real,allocatable,DIMENSION (:)::z
real,allocatable,dimension (:,:,:)::xx,yy,zz,mask
!real,dimension(nx,ny,nz)::xx,yy,zz,mask
nx=150
ny=109
nz=109
allocate(x(nx))
allocate(y(ny))
allocate(z(nz))
allocate(xx(nx,ny,nz))
allocate(yy(nx,ny,nz))
allocate(zz(nx,ny,nz))
allocate(mask(nx,ny,nz))
lx=8.0
ly=4.0
lz=4.0
potx1=1.0
potx2=1.0
poty1=1.0
poty2=1.0
potz1=1.0
potz2=1.0

px1=lx/8.
px2=px1+1.
py1=ly/2.-0.15
py2=ly/2.+0.15
pz1=lz/2.-0.15
pz2=lz/2.+0.15
capa=0.1*(py2-py1)
pend=(pz2-pz1)/(px2-px1)
!ind=pz1-pend*px1
!write(*,*)'m',pend,'b',ind
!         ec2=pz1
!         ec3=px2
write(*,*)ny/2,nz/2
do i=1,nx
    x(i)=lx*(float(i-1)/float(nx-1))**potx1
end do
do j=1,ny
    y(j)=ly*(float(j-1)/float(ny-1))**poty1
end do
do k=1,nz
    z(k)=lz*(float(k-1)/float(nz-1))**potz1
end do
!do i=1,110
!    x(40+i)=lx*(1.-1./8.)*(float(i)/float(110))**potx2+x(40)
!end do
!do j=1,50
!     y(j)=(py1-capa)*(float(j-1)/float(50-1))**poty1
!     write(*,*)j,y(j)
!end do
!do j=1,20
!     y(50+j)=(py2-py1+2.*capa)*(float(j)/float(20-1))**1.+y(50)
!     write(*,*)j+50,y(j+50)-y(j+50-1)
!end do
!do j=1,39
!     y(70+j)=(ly-py2-capa)*(float(j)/float(39-1))**poty2+y(70)
!     write(*,*)70+j,y(70+j)-y(70+j-1)
!end do
!
!do j=1,50
!     z(j)=(pz1-capa)*(float(j-1)/float(50-1))**potz1
!!     write(*,*)j,z(j)
!end do
!do j=1,20
!     z(50+j)=(pz2-pz1+2.*capa)*(float(j)/float(20-1))**1.+z(50)
!!     write(*,*)j+50,z(j+50)-z(j+50-1)
!end do
!do j=1,39
!     z(70+j)=(lz-pz2-capa)*(float(j)/float(39-1))**potz2+y(70)
!     write(*,*)70+j,z(70+j)
!end do
!!write(*,*)'Escribiendo ASCII...'
!
nv=5   

open(54,file='ascii_malla.dat')
    write(54,*)'variables = "x", "y", "z", "body"'
    write(54,*)'zone I=',nx,'J=',ny,"K=",nz,' datapacking=point'
    do k=1,nz
       do j=1,ny
          do i=1,nx
             xx(i,j,k)=x(i)
             yy(i,j,k)=y(j)
             zz(i,j,k)=z(k)

!         ec1=pend*xx(i,j,k)+ind
!         mask(i,j,k)=1.0
!         if((zz(i,j,k).le.ec1).and.(zz(i,j,k).ge.ec2).and.(xx(i,j,k).ge.px1).and.(xx(i,j,k).le.px2).and.(yy(i,j,k).ge.py1).and.(yy(i,j,k).le.py2))mask(i,j,k)=0.0
!         if((xx(i,j,k).ge.px1).and.(xx(i,j,k).le.px2).and.(yy(i,j,k).ge.py1).and.(yy(i,j,k).le.py2).and.(zz(i,j,k).ge.pz1).and.(zz(i,j,k).le.pz2))mask(i,j,k)=0.0
!             write(54,*)xx(i,j,k),yy(i,j,k),zz(i,j,k),mask(i,j,k)
!   if(yy(i,j,k).eq.2.0)write(*,*)yy(i,j,k)
!   if(zz(i,j,k).eq.2.0)write(*,*)zz(i,j,k)
          end do
       end do
    end do
close(54)
nv=5   

write(*,*)'Escribiendo binario ...'
open(121,file='jet.grid',form='unformatted')
     write(121)nv
     write(121)nx,ny,nz
     write(121)xx
     write(121)yy
     write(121)zz
close(121)

deallocate(x)
deallocate(y)
deallocate(z)
deallocate(xx)
deallocate(yy)
deallocate(zz)
deallocate(mask)

end
